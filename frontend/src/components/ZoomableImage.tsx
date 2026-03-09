import { useCallback, useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

interface Props extends React.ImgHTMLAttributes<HTMLImageElement> {}

export default function ZoomableImage(props: Props) {
  const [open, setOpen] = useState(false);

  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open, close]);

  return (
    <>
      {/* biome-ignore lint: click handler on image for lightbox */}
      <img {...props} onClick={() => setOpen(true)} style={{ ...props.style, cursor: 'zoom-in' }} />
      {open &&
        createPortal(
          // biome-ignore lint: overlay click to close
          <div className="lightbox-overlay" onClick={close}>
            <img
              className="lightbox-image"
              src={props.src}
              alt={props.alt}
              onClick={(e) => e.stopPropagation()}
            />
          </div>,
          document.body,
        )}
    </>
  );
}
