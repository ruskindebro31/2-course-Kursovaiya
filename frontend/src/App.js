import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App">
          <header className="App-header">
            <h1>Candels Project - Trajectory В</h1>
          </header>
          <main>
            {/* Здесь будут ваши компоненты */}
          </main>
        </div>
      </Router>
      <ToastContainer />
    </QueryClientProvider>
  );
}

export default App;
