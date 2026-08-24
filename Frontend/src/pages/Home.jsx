import { useEffect, useState } from 'react';
import TicketForm from '../components/TicketForm';
import ResultCard from '../components/ResultCard';
import History from '../components/History';
import SearchBar from '../components/SearchBar';
import { classifyTicket, getTicketHistory } from '../services/api';

function Home() {
  const [ticketText, setTicketText] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [historyLoading, setHistoryLoading] = useState(false);

  const fetchHistory = async (searchValue = '') => {
    setHistoryLoading(true);
    setError('');

    try {
      const data = await getTicketHistory(searchValue);
      setHistory(Array.isArray(data) ? data : []);
    } catch (err) {
      const message = getErrorMessage(err, 'Unable to load history.');
      setError(message);
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleAnalyze = async () => {
    if (!ticketText.trim()) {
      setError('Please enter a ticket before analyzing.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await classifyTicket(ticketText.trim());
      setResult(data);
      await fetchHistory('');
    } catch (err) {
      const message = getErrorMessage(err, 'Unable to classify the ticket.');
      setError(message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    await fetchHistory(search.trim());
  };

  const getErrorMessage = (err, fallback) => {
    if (!err) return fallback;

    const status = err?.response?.status;
    const data = err?.response?.data;
    const detail = data?.detail || data?.error || data?.details;

    if (status === 404) {
      return 'The backend endpoint could not be found.';
    }

    if (status === 502) {
      return detail || 'Gemini classification is currently unavailable. Please try again later.';
    }

    if (status === 500 || detail?.toLowerCase().includes('gemini')) {
      return 'Gemini API error. Please try again later.';
    }

    if (err.code === 'ERR_NETWORK' || err.message?.includes('Network')) {
      return 'Network error. Please check if the backend is running.';
    }

    if (detail) {
      return detail;
    }

    return fallback;
  };

  return (
    <div className="container py-4 py-lg-5">
      <div className="row g-4">
        <div className="col-12">
          <div className="p-4 rounded-4 bg-white shadow-sm">
            <h2 className="fw-bold mb-2">AI-powered support ticket analysis</h2>
            <p className="text-muted mb-0">
              Classify incoming tickets, estimate urgency, and generate a suggested responder.
            </p>
          </div>
        </div>

        {error && (
          <div className="col-12">
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          </div>
        )}

        <div className="col-lg-7">
          <TicketForm
            ticketText={ticketText}
            onTicketChange={setTicketText}
            onAnalyze={handleAnalyze}
            loading={loading}
            disabled={ticketText.trim().length === 0}
          />
        </div>

        <div className="col-lg-5">
          {result ? <ResultCard result={result} /> : <div className="card card-shadow h-100"><div className="card-body text-muted">Your classification result will appear here.</div></div>}
        </div>

        <div className="col-12">
          <div className="card card-shadow">
            <div className="card-body">
              <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-3">
                <h5 className="card-title mb-0">Ticket History</h5>
                <SearchBar value={search} onChange={setSearch} onSearch={handleSearch} loading={historyLoading} />
              </div>
              <History tickets={history} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
