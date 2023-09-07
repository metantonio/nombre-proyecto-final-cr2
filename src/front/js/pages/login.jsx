import React, { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext";
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { store, actions } = useContext(Context);
  let navigate = useNavigate(""); // useHistory("")

  const register = async () => {
    //Sección de verificación
    if (password == "" || email == "") {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Por favor llene ambos campos!",
        /* footer: '<a href="">Why do I have this issue?</a>' */
        timer: 3500,
      });
      return;
    }

    //Sección para enviar la data al backend
    let obj = {
      email: email,
      password: password,
    };

    let response = await actions.fetchPromise("/api/login", "POST", obj);

    if (response.ok) {
      let responseJson = await response.json();
      console.log(responseJson);
      Swal.fire({
        position: "center",
        icon: "success",
        title: responseJson.message,
        showConfirmButton: false,
        timer: 1500,
      });
      localStorage.setItem("token", responseJson.token);
      actions.activateLoginConfirmation();
      navigate("/inventada"); // history.push("/")
    } else {
      let responseJson = await response.json();
      console.log(responseJson);
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Error al registrar!",
        /* footer: '<a href="">Why do I have this issue?</a>' */
        timer: 3500,
      });
    }
    return;
  };

  return (
    <>
      <div className="container">
        <div className="row d-flex">
          <div className="col-sm-6 col-md-4">
            <span>Email:</span>
          </div>
          <div className="col-sm-6 col-md-4">
            <input
              placeholder="email"
              onChange={(e) => {
                setEmail(e.target.value);
              }}
            ></input>
          </div>
        </div>
        <div className="row d-flex">
          <div className="col-sm-6 col-md-4">
            <span>Password</span>
          </div>
          <div className="col-sm-6 col-md-4">
            <input
              placeholder="password"
              onChange={(e) => {
                setPassword(e.target.value);
              }}
              type="password"
            ></input>
          </div>
        </div>
        <div className="row d-flex">
          <button type="button" onClick={register}>
            Login
          </button>
        </div>
      </div>
    </>
  );
};

export default Login;
