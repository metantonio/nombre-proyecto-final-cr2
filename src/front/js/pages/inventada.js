import React from "react";
import WithAuth from "../component/Auth/WithAuth";
import UploadImage from "../component/uploadImage.jsx";

const Inventada = () => {
    return(<>
    <h1>Suba su imagen de Perfil</h1>
    <br/>
    <UploadImage />
    </>)
}

export default WithAuth(Inventada);