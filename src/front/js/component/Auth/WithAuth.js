import React, {useContext} from "react";
import { Context } from "../../store/appContext";
import { Navigate } from "react-router-dom";

//H.O.C 
const WithAuth = (Component) => {

    const AuthRoute = () => {
        const {store, actions} = useContext(Context);

        const isAuth = store.loginConfirmation
        if(isAuth){
            return <Component />
        }else{
            return <Navigate to="/" />
        }
    }
    return AuthRoute

}

export default WithAuth