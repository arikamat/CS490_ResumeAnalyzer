import {createBrowserRouter, RouterProvider } from 'react-router-dom'
import SignUp from './pages/SignUp/SignUp.jsx'; 
import Login  from './pages/Login/Login.jsx';
import Home from './pages/Home/Home.jsx';
const router = createBrowserRouter([
    {
        path: '/',
        element: <Home/>,
        errorElement: <div>404 Not Found</div>
    },
    {
        path: '/login',
        element: <Login/>
    },
    {
        path: '/register',
        element:<SignUp/>
    }
]);

function App(){
    return (
        <div>
            <RouterProvider router={router}/>
        </div>
    )
}

export default App;