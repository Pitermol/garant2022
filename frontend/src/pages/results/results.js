import "../styles.css";
import logo from "../static/logo.png"
import back from "../static/back.png"
import next from "../static/Vector.png"
import doc from "../static/doc.png"
import download from "../static/download.png"
import enlarge from "../static/enlarge.png"

export default function Results() {

    return (
        <body>
        <header>
            <div>
                <img src={logo} alt="Logo" width="20%" class="logo_img"></img>
            </div>
        </header>
        <main style={{height: "800px"}}>
            <div style={{display: "flex", flexDirection: "row", marginLeft: "2%"}}>
                <a href="/dates" style={{textDecoration: "none"}}><button className="btn_back" style={{marginTop: "30px"}}><img src={back} alt="img" style={{marginRight: "5px", marginTop: "3px"}}></img>Назад</button></a>
            </div>
            <div id="docs_list_div">
                <div id="docs_list_div_header">
                    <h>Файл</h>
                    <h style={{marginLeft: "31.5%"}}>Действующие</h>
                    <h style={{marginLeft: "8%"}}>С изменениями</h>
                    <h style={{marginLeft: "8%"}}>Недействующие</h>
                </div>
                <ul style={{marginTop: "1.6%", padding: "0", width: "91%", height: "84%", overflowY: "scroll", overflowX: "hidden"}}>
                    <li class="ready_docs_list_item">
                        <div style={{display: "flex", flexDirection: "column", width: "33%", height: "auto"}}>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <img src={doc} alt="doc" width="30px" height="37px"></img>
                                <h style={{marginLeft: "2%"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                            </div>
                            <h style={{fontSize: "14px", color: "#8D8D8D", fontWeight: "500", margin: "1% 7%"}}>150мб, 02.02.2022, 17:45</h>
                        </div>
                        
                        <div className="active_docs"><h className="active_docs_text">47 действующих</h></div>
                        <div className="changed_docs"><h className="changed_docs_text">5 изменнившихся</h></div>
                        <div className="inactive_docs"><h className="inactive_docs_text">3 недействующих</h></div>
                        {/* <div className="download_result"><img src={download} alt="img"></img><a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "2%", color: "#3272C0"}}>Скачать отчет</a></div> */}
                        <a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "4%", color: "#3272C0", width: "10%"}}><div className="download_result"><img src={download} alt="img"></img>Скачать отчет</div></a>
                        
                    </li>
                    <li class="ready_docs_list_item">
                        <div style={{display: "flex", flexDirection: "column", width: "33%", height: "auto"}}>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <img src={doc} alt="doc" width="30px" height="37px"></img>
                                <h style={{marginLeft: "2%"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                            </div>
                            <h style={{fontSize: "14px", color: "#8D8D8D", fontWeight: "500", margin: "1% 7%"}}>150мб, 02.02.2022, 17:45</h>
                        </div>
                        
                        <div className="active_docs"><h className="active_docs_text">47 действующих</h></div>
                        <div className="changed_docs"><h className="changed_docs_text">5 изменнившихся</h></div>
                        <div className="inactive_docs"><h className="inactive_docs_text">3 недействующих</h></div>
                        {/* <div className="download_result"><img src={download} alt="img"></img><a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "2%", color: "#3272C0"}}>Скачать отчет</a></div> */}
                        <a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "4%", color: "#3272C0", width: "10%"}}><div className="download_result"><img src={download} alt="img"></img>Скачать отчет</div></a>
                    </li>
                    <li class="ready_docs_list_item">
                        <div style={{display: "flex", flexDirection: "column", width: "33%", height: "auto"}}>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <img src={doc} alt="doc" width="30px" height="37px"></img>
                                <h style={{marginLeft: "2%"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                            </div>
                            <h style={{fontSize: "14px", color: "#8D8D8D", fontWeight: "500", margin: "1% 7%"}}>150мб, 02.02.2022, 17:45</h>
                        </div>
                        
                        <div className="active_docs"><h className="active_docs_text">47 действующих</h></div>
                        <div className="changed_docs"><h className="changed_docs_text">5 изменнившихся</h></div>
                        <div className="inactive_docs"><h className="inactive_docs_text">3 недействующих</h></div>
                        {/* <div className="download_result"><img src={download} alt="img"></img><a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "2%", color: "#3272C0"}}>Скачать отчет</a></div> */}
                        <a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "4%", color: "#3272C0", width: "10%"}}><div className="download_result"><img src={download} alt="img"></img>Скачать отчет</div></a>
                    </li>
                    <li class="ready_docs_list_item">
                        <div style={{display: "flex", flexDirection: "column", width: "33%", height: "auto"}}>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <img src={doc} alt="doc" width="30px" height="37px"></img>
                                <h style={{marginLeft: "2%"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                            </div>
                            <h style={{fontSize: "14px", color: "#8D8D8D", fontWeight: "500", margin: "1% 7%"}}>150мб, 02.02.2022, 17:45</h>
                        </div>
                        
                        <div className="active_docs"><h className="active_docs_text">47 действующих</h></div>
                        <div className="changed_docs"><h className="changed_docs_text">5 изменнившихся</h></div>
                        <div className="inactive_docs"><h className="inactive_docs_text">3 недействующих</h></div>
                        {/* <div className="download_result"><img src={download} alt="img"></img><a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "2%", color: "#3272C0"}}>Скачать отчет</a></div> */}
                        <a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "4%", color: "#3272C0", width: "10%"}}><div className="download_result"><img src={download} alt="img"></img>Скачать отчет</div></a>
                    </li>
                    <li class="ready_docs_list_item">
                        <div style={{display: "flex", flexDirection: "column", width: "33%", height: "auto"}}>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <img src={doc} alt="doc" width="30px" height="37px"></img>
                                <h style={{marginLeft: "2%"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                            </div>
                            <h style={{fontSize: "14px", color: "#8D8D8D", fontWeight: "500", margin: "1% 7%"}}>150мб, 02.02.2022, 17:45</h>
                        </div>
                        
                        <div className="active_docs"><h className="active_docs_text">47 действующих</h></div>
                        <div className="changed_docs"><h className="changed_docs_text">5 изменнившихся</h></div>
                        <div className="inactive_docs"><h className="inactive_docs_text">3 недействующих</h></div>
                        {/* <div className="download_result"><img src={download} alt="img"></img><a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "2%", color: "#3272C0"}}>Скачать отчет</a></div> */}
                        <a href="https://yandex.ru" style={{textDecoration: "none", marginLeft: "4%", color: "#3272C0", width: "10%"}}><div className="download_result"><img src={download} alt="img"></img>Скачать отчет</div></a>
                    </li>
                </ul>
            </div>
        </main>
    </body>
    );
}