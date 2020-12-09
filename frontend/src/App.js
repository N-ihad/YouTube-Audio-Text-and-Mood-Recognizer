import logo from "./logo.svg";
import "./App.css";
import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Form } from "react-bootstrap";
import Button from "react-bootstrap/Button";
import axios from "axios";
import RingLoader from "react-spinners/RingLoader";
import FileDownload from "js-file-download";

const styles = {
  loading: {
    transform: "translate(-50%, -50%)",
    left: "50%",
    top: "50%",
    filter: "brightness(100%) !important",
    zIndex: "10000",
    position: "absolute",
  },
};

function App() {
  const [link, setLink] = useState();
  const [wordSearch, setWordSearch] = useState();
  const [emotionSearch, setEmotionSearch] = useState();
  const [loading, setLoading] = useState(false);

  const handleYTLinkSubmit = () => {
    setLoading(true);
    axios
      .post(
        "http://localhost:5002/generate-files",
        { link: link },
        { responseType: "blob" },
        {
          headers: {
            accept: "application/json",
            "Accept-Language": "en-US,en;q=0.8",
          },
        }
      )
      .then((response) => {
        setLoading(false);
        FileDownload(response.data, "samples.zip");
        alert("Всё прошло успешно! Архив подан на скачку.");
      })
      .catch((error) => {
        setLoading(false);
        console.log(error);
        alert(error);
      });
  };

  const handleFilterByWordSubmit = () => {
    setLoading(true);
    axios
      .post(
        "http://localhost:5002/generate-files-by-word",
        { wordSearch: wordSearch },
        { responseType: "blob" },
        {
          headers: {
            accept: "application/json",
            "Accept-Language": "en-US,en;q=0.8",
          },
        }
      )
      .then((response) => {
        setLoading(false);
        FileDownload(response.data, "samples_sentence.zip");
        alert("Всё прошло успешно! Архив подан на скачку.");
      })
      .catch((error) => {
        setLoading(false);
        console.log(error);
        alert(error);
      });
  };

  const handleFilterByEmotionSubmit = () => {
    setLoading(true);
    axios
      .post(
        "http://localhost:5002/generate-files-by-emotion",
        { emotionSearch: emotionSearch },
        { responseType: "blob" },
        {
          headers: {
            accept: "application/json",
            "Accept-Language": "en-US,en;q=0.8",
          },
        }
      )
      .then((response) => {
        setLoading(false);
        FileDownload(response.data, "samples_emotion.zip");
        alert("Всё прошло успешно! Архив подан на скачку.");
      })
      .catch((error) => {
        setLoading(false);
        console.log(error);
        alert(error);
      });
  };

  return (
    <div className="App">
      <header
        className={loading ? "App-header App-header-disabled" : "App-header"}
      >
        <img src={logo} className="App-logo" alt="logo" />
        <div style={{ width: "600px", marginBottom: "20px" }}>
          <label htmlFor="example1">Ссылка на YouTube видео</label>
          <Form.Control
            size="lg"
            type="text"
            placeholder="Например: https://www.youtube.com/watch?v=9Onnyfu6yvo"
            onChange={(e) => {
              setLink(e.target.value);
            }}
          />
          <Button
            variant="outline-info"
            size="lg"
            block
            onClick={handleYTLinkSubmit}
            style={{ marginTop: "15px" }}
          >
            Скачать семплы
          </Button>
        </div>
        <div style={{ width: "600px", marginBottom: "20px" }}>
          <label htmlFor="example1">Фильтрация семплов по слову</label>
          <Form.Control
            size="lg"
            type="text"
            placeholder="Например: машина"
            onChange={(e) => {
              setWordSearch(e.target.value);
            }}
          />
          <Button
            variant="outline-info"
            size="lg"
            block
            onClick={handleFilterByWordSubmit}
            style={{ marginTop: "15px" }}
          >
            Скачать семплы
          </Button>
        </div>
        <div style={{ width: "600px", marginBottom: "20px" }}>
          <label htmlFor="example1">Фильтрация семплов по эмоции</label>
          <Form.Control
            size="lg"
            type="text"
            placeholder="Например: angry"
            onChange={(e) => {
              setEmotionSearch(e.target.value);
            }}
          />
          <Button
            variant="outline-info"
            size="lg"
            block
            onClick={handleFilterByEmotionSubmit}
            style={{ marginTop: "15px" }}
          >
            Скачать семплы
          </Button>
        </div>
      </header>
      {loading && (
        <RingLoader
          css={styles.loading}
          size={250}
          color={"#0dcf9b"}
          loading={loading}
        />
      )}
    </div>
  );
}

export default App;
