import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import IdeaWorkspace from './pages/IdeaWorkspace'

function App() {
    return (
        <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/idea/:id" element={<IdeaWorkspace />} />
        </Routes>
    )
}

export default App
