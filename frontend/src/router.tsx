import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Home from "./pages/Home";
import Customers from "./pages/Customers";
import Registry from "./pages/Registry";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* layout */}
        <Route path="/" element={<App />}>
          {/* / */}
          <Route index element={<Home />} />
          {/* /customers */}
          <Route path="customers" element={<Customers />} />
          {/* /registry */}
          <Route path="registry" element={<Registry />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
