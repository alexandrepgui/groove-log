import { useCallback, useEffect, useState } from 'react';
import { getAuthStatus, logout, startOAuthLogin } from '../api';
import type { AuthStatus } from '../types';

export default function DiscogsAuth() {
  const [status, setStatus] = useState<AuthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchStatus = useCallback(async () => {
    try {
      const s = await getAuthStatus();
      setStatus(s);
    } catch {
      // Auth endpoint unavailable — likely no OAuth configured
    }
  }, []);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  // Listen for the popup closing message after OAuth completes
  useEffect(() => {
    const handler = (e: MessageEvent) => {
      if (e.origin !== window.location.origin) return;
      if (e.data?.type === 'discogs-oauth-complete') {
        fetchStatus();
      }
    };
    window.addEventListener('message', handler);
    return () => window.removeEventListener('message', handler);
  }, [fetchStatus]);

  if (!status || !status.oauth_configured) return null;

  const handleLogin = async () => {
    setLoading(true);
    setError(null);
    try {
      const authorizeUrl = await startOAuthLogin();
      // Open Discogs authorization in a popup
      window.open(authorizeUrl, 'discogs-oauth', 'width=600,height=700');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to start login');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      setStatus({ ...status, authenticated: false, username: null });
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to logout');
    }
  };

  if (status.authenticated) {
    return (
      <div className="discogs-auth">
        <span className="auth-user">Connected as <strong>{status.username ?? 'Discogs user'}</strong></span>
        <button className="btn btn-auth-logout" onClick={handleLogout}>Disconnect</button>
      </div>
    );
  }

  return (
    <div className="discogs-auth">
      <button className="btn btn-auth-login" onClick={handleLogin} disabled={loading}>
        {loading ? 'Connecting...' : 'Connect to Discogs'}
      </button>
      {error && <span className="auth-error">{error}</span>}
    </div>
  );
}
