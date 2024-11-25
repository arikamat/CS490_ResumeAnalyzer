import React from 'react';
import {Navigate} from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function PrivateRoute ({Component}){
    const { isAuth} = useAuth();
    return isAuth ? <Component/> : <Navigate to="/login" replace />
}

export default PrivateRoute;