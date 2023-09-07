import React, { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext";

const UploadImage = () => {
  const [files, setFiles] = useState(null);

  const uploadImage = async (evt) => {
    evt.preventDefault();
    // we are about to send this to the backend.
    //console.log("These are the files", files);
    let body = new FormData();
    body.append("profile_image", files[0]);

    let casa = { direccion: "Avenida ABC", country: "CR" };
    body.append("info", JSON.stringify(casa));
    //console.log("valor del body: ", body.data, body.profile_image);
    const options = {
      body,
      method: "PUT",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    };

    let response = await fetch(
      `${process.env.BACKEND_URL}/api/user/upload-image`,
      options
    );

    if (response.ok) {
      let responseJson = await response.json();
      console.log(responseJson);
    } else {
      let responseJson = await response.json();
      console.log(responseJson);
      alert("error");
    }
  };

  return (
    <div className="jumbotron">
      <form onSubmit={uploadImage}>
        <input type="file" onChange={(e) => setFiles(e.target.files)} />
        <button>Upload</button>
      </form>
    </div>
  );
};

export default UploadImage;
