function ResultCard({ result }) {
  const getPriorityClass = (priority) => {
    const normalized = (priority || '').toLowerCase();
    if (normalized === 'high') return 'badge-priority-high';
    if (normalized === 'medium') return 'badge-priority-medium';
    return 'badge-priority-low';
  };

  const confidence = Number(result?.confidence ?? 0);

  return (
    <div className="card card-shadow h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-3">
          <div>
            <h5 className="card-title mb-1">Classification Result</h5>
            <p className="text-muted small mb-0">{result?.created_time || 'Recently analyzed'}</p>
          </div>
          <span className={`badge rounded-pill ${getPriorityClass(result?.priority)}`}>
            {result?.priority || 'Unknown'}
          </span>
        </div>

        <div className="row g-3">
          <div className="col-md-6">
            <p className="mb-1 fw-semibold">Category</p>
            <p className="text-primary mb-0">{result?.category || 'N/A'}</p>
          </div>
          <div className="col-md-6">
            <p className="mb-1 fw-semibold">Suggested Owner</p>
            <p className="text-primary mb-0">{result?.suggested_owner || 'N/A'}</p>
          </div>
          <div className="col-md-6">
            <p className="mb-1 fw-semibold">Confidence</p>
            <div className="progress" style={{ height: '10px' }}>
              <div
                className="progress-bar bg-success"
                role="progressbar"
                style={{ width: `${Math.min(Math.max(confidence, 0), 100)}%` }}
                aria-valuenow={confidence}
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
            <small className="text-muted">{confidence}%</small>
          </div>
          <div className="col-md-6">
            <p className="mb-1 fw-semibold">Sentiment</p>
            <p className="mb-0">{result?.sentiment || 'N/A'}</p>
          </div>
          <div className="col-12">
            <p className="mb-1 fw-semibold">Reason</p>
            <p className="mb-0">{result?.reason || 'No reason provided.'}</p>
          </div>
          <div className="col-12">
            <p className="mb-1 fw-semibold">AI Reply</p>
            <p className="mb-0">{result?.ai_reply || 'No reply generated.'}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
