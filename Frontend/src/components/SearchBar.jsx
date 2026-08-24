function SearchBar({ value, onChange, onSearch, loading }) {
  return (
    <div className="input-group shadow-sm">
      <input
        type="text"
        className="form-control"
        placeholder="Search ticket history..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && onSearch()}
      />
      <button className="btn btn-outline-primary" type="button" onClick={onSearch} disabled={loading}>
        {loading ? <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> : 'Search'}
      </button>
    </div>
  );
}

export default SearchBar;
