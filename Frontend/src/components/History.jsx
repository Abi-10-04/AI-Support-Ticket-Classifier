function History({ tickets }) {
  return (
    <div className="card card-shadow h-100">
      <div className="card-body">
        <h5 className="card-title mb-3">Ticket History</h5>

        {tickets.length === 0 ? (
          <div className="text-muted">No tickets found.</div>
        ) : (
          <div className="d-flex flex-column gap-3">
            {tickets.map((ticket, index) => (
              <div key={ticket.id || index} className="border rounded p-3">
                <div className="d-flex justify-content-between align-items-start gap-2">
                  <h6 className="mb-1">{ticket.ticket_text || 'Untitled ticket'}</h6>
                  <span className="badge bg-light text-dark">{ticket.created_time || 'Unknown'}</span>
                </div>
                <div className="small text-muted mb-2">{ticket.category || 'Unknown category'}</div>
                <div className="d-flex flex-wrap gap-2">
                  <span className="badge bg-primary">{ticket.priority || 'Unknown'}</span>
                  <span className="badge bg-secondary">Owner: {ticket.owner || 'N/A'}</span>
                  <span className="badge bg-info text-dark">{ticket.sentiment || 'N/A'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default History;
