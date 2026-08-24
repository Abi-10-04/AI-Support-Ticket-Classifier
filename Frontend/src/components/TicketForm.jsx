function TicketForm({ ticketText, onTicketChange, onAnalyze, loading, disabled }) {
  return (
    <div className="card card-shadow h-100">
      <div className="card-body">
        <h5 className="card-title mb-3">Analyze a Ticket</h5>
        <label htmlFor="ticketText" className="form-label">Support Ticket</label>
        <textarea
          id="ticketText"
          className="form-control"
          rows="10"
          placeholder="Paste customer support ticket here..."
          value={ticketText}
          onChange={(e) => onTicketChange(e.target.value)}
        />
        <div className="d-flex justify-content-between align-items-center mt-3">
          <button className="btn btn-primary" onClick={onAnalyze} disabled={loading || disabled}>
            {loading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Analyzing...
              </>
            ) : (
              'Analyze Ticket'
            )}
          </button>
          <small className="text-muted">{ticketText.trim().length} characters</small>
        </div>
      </div>
    </div>
  );
}

export default TicketForm;
