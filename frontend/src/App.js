import Dates from "./pages/dates/dates";
import {
    BrowserRouter,
    Routes,
    Route,
  } from "react-router-dom";
import Results from "./pages/results/results";
import Start from "./pages/start/start";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Start />} />
                <Route path="/dates" element={<Dates />} />
                <Route path="/results" element={<Results />} />
            </Routes>
        </BrowserRouter>
    )
  }

export default App;
