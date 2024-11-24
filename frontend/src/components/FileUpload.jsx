import { useState } from 'react'
import './FileUpload.css'

function App() {
  return (
    <div className="App">
        <form>
          <h1>React File Upload</h1>
          <input type="file" />
          <button type="submit">Upload</button>
        </form>
    </div>
  );
}

export default App
