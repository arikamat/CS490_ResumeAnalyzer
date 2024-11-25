import {jwtDecode} from 'jwt-decode'

function isJWTValid(){
    const token = localStorage.getItem('token');
    if(!token){
        return false;
    }
    try{
        const decodedJWT = jwtDecode(token);
        const valid = decodedJWT.exp *1000 > Date.now();
        return valid;
    }
    catch(err){
        return false;
    }
}

export default isJWTValid;