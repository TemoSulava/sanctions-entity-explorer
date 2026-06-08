import styles from "./StatusMessage.module.css";

export type StatusVariant = "loading" | "error" | "empty" | "idle";

interface StatusMessageProps {
  variant: StatusVariant;
  title: string;
  detail?: string;
}

const GLYPHS: Record<StatusVariant, string> = {
  loading: "◍",
  error: "▲",
  empty: "○",
  idle: "⌕",
};

export function StatusMessage({ variant, title, detail }: StatusMessageProps) {
  return (
    <div
      className={styles.wrap}
      data-variant={variant}
      role={variant === "error" ? "alert" : "status"}
    >
      <span className={styles.glyph} aria-hidden="true">
        {GLYPHS[variant]}
      </span>
      <p className={styles.title}>{title}</p>
      {detail ? <p className={styles.detail}>{detail}</p> : null}
    </div>
  );
}
