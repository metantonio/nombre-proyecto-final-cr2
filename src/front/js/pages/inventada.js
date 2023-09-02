import React from "react";
import WithAuth from "../component/Auth/WithAuth";

const Inventada = () => {
    return(<>
    <h1>Soy una vista protegida</h1>
    </>)
}

export default WithAuth(Inventada);