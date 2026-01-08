import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { TranslationPage } from './pages/TranslationPage';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/translate" element={<TranslationPage />} />
            </Routes>
        </Router>
    );
}

export default App;
