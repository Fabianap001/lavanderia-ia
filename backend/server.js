const express = require("express");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
const FormData = require("form-data");

const app = express();
const upload = multer({ storage: multer.memoryStorage() });

app.use(cors());
app.use(express.json());

app.post("/analizar", upload.single("imagen"), async (req, res) => {
  try {
    const formData = new FormData();
    formData.append("imagen", req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype,
    });

    const respuesta = await axios.post(
      "http://127.0.0.1:8000/analizar",
      formData,
      { headers: formData.getHeaders() }
    );

    res.json(respuesta.data);
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Error al analizar la imagen" });
  }
});

app.listen(3000, () => {
  console.log("Servidor Node.js corriendo en http://localhost:3000");
});