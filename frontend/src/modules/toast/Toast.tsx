

export interface ToastProps {
    type: 'primary' | 'success' | 'warning' | 'danger' |'info'
    color: string
    content: string
    show: boolean
    onClose: () => void
}

const ToastComponent: React.FC<ToastProps> = (props) => {
    const { type, color, content, show, onClose } = props

    return (
        <div className={`toast-container position-fixed bottom-0 end-0 p-3 ${show ? 'show' : ''}`} style={{ zIndex: 11 }}>
            <div className={`toast show`} role="alert" aria-live="assertive" aria-atomic="true" style={{ backgroundColor: color }}>
                <div className="toast-header">
                    <strong className="me-auto">Bootstrap - {type}</strong>
                    <small>Just now</small>
                    <button type="button" className="btn-close" onClick={onClose} aria-label="Close"></button>
                </div>
                <div className="toast-body">
                    {content}
                </div>
            </div>
        </div>
    );
}

export default ToastComponent