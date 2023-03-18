import HomePage from "./components/HomePage";
import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  const renderHomePage = () => {
    return <HomePage />;
  };

  return (
    <Router>
      <Routes>
        <Route exact path="/" element={renderHomePage()} />
      </Routes>
    </Router>
  );
}

export default App;
