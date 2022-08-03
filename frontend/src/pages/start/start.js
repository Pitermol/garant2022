import "../styles.css";
import Vector from "../static/Vector.png";
import g from "../static/g.png";
import add1 from "../static/add1(1).png";
import logo from "../static/logo.png";

export default function Start() {

    return (
        <body>
            <header>
                <div>
                    <img src={logo} alt="Logo" width="20%" class="logo_img"></img>
                </div>
            </header>
            <main>
                <div id="upload_files_up">
            <div className="upload_page_info">
                <span className="upload_files_title" style={{width: "180px"}}>Загрузка файлов</span>
                <span className="steps_counter">(Шаг 1 из 2)</span>
            </div>
            <div style={{display: "flex", flexDirection: "row", marginRight: "2%"}}>
                <a style={{textDecoration: "none"}} href="/dates"><button id="btn_next_1" className="btn_next">Далее  <img alt="img" src={Vector} style={{marginLeft: "5px", marginTop:"3px"}}></img></button></a>
            </div>
        </div>
        <div id="big_rows">
                <div id="dragon_drop">
                    <div>
                        <div id="folder">
                            <img src={g} alt="img" id="folder"></img>
                            <h5>Здесь пока ничего нет</h5>
                        </div>
                        <div id="drop">
                            <div id="dashed_upload">
                                <span id="instructions_upload">Перетащите файлы или <a href="https://yandex.ru" style={{textDecoration: "none"}}>загрузите</a></span>
                                <span id="supported_formats" style={{color: "#B1B9C3"}}>Поддерживаемые форматы: png, jpg</span>
                                <button onClick={() => {}} id="btn_add_files">
                                    <img id="add1" src={add1} alt="img"></img>
                                    <h style={{marginBottom: "2px", position: "relative"}}>загрузить файл</h>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div hidden id="loading" style={{backgroundColor: "#F4F5F7", marginLeft: "20%", width: "600px", marginTop: "2%", height: "90%"}}>
                        <div id="progress_bar" style={{backgroundColor: "#3272C0", width: "100%", height: "100px", borderRadius: "8px"}}>
                        </div>
                    </div>
                </div>
            </div></main></body>
    );
}