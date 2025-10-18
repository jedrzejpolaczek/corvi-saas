import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Experiments from './pages/Experiments';

function App() {
  console.log('🔥 App component started!');
  
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    console.log('🔥 App useEffect - checking token...');
    // Sprawdź czy user jest zalogowany
    const token = localStorage.getItem('token');
    console.log('Token:', token);
    if (token === 'demo_token_12345') {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    console.log('🔥 handleLogin called!');
    setIsAuthenticated(true);
  };

  console.log('🔥 App rendering, isAuthenticated:', isAuthenticated);

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return <Experiments />;
}

export default App;