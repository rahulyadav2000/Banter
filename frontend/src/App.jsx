import "./App.css";
//import Home from "./pages/Home.jsx";
//import Register from "./pages/Register.jsx";
import { RouterProvider } from "react-router-dom";
import { route } from "./router/route.jsx";

function App() {
  return (
    <>
      <RouterProvider router={route} />
      {/* <Home /> */}
    </>
  );
}

export default App;
