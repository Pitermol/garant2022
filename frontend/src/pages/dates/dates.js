import logo from "../static/logo.png"
import back from "../static/back.png"
import next from "../static/Vector.png"
import doc from "../static/doc.png"
import calendar from "../static/date_range.png"
import c51 from "../static/Component 51.png"
import c52 from "../static/Component 52.png"
import c53 from "../static/Component 53.png"
import close from "../static/close.png"

function Dates() {
    return (
      <body>
        <header>
            <div>
                <img src={logo} alt="Logo" width="20%" className="logo_img"></img>
            </div>
        </header>
        <main>
            <div id="upload_files_up">
                <div style={{display: "flex", flexDirection: "row", marginLeft: "2%"}}>
                    <a href="/" style={{textDecoration: "none"}}><button className="btn_back"><img src={back} style={{marginRight: "5px", marginTop: "3px"}} alt="img"></img>Назад</button></a>
                </div>
                <div className="upload_page_info">
                    <span className="upload_files_title" style={{width: "430px"}}>Выбор даты для проверки действия НПА</span>
                    <span className="steps_counter">(Шаг 2 из 2)</span>
                </div>
                <div style={{display: "flex", flexDirection: "row", marginRight: "2%"}}>
                    <a href="/results" style={{textDecoration: "none"}}><button id="btn_next_2" className="btn_next">Далее  <img src={next} alt="img" style={{marginLeft: "5px", marginTop:"5px"}}></img></button></a>
                </div>
            </div>
            <div className="docs_list_block">
                <div style={{display: "flex", width: "920px", height: "100%"}}>
                    <ul className="docs_list">
                        <li className="docs_list_element">
                            <div style={{display: "flex", flexDirection: "row", height: "100%"}}>
                                <div style={{display: "flex", flexDirection: "row"}}>
                                    <img src={doc} alt="doc" width="55px" height="50px"></img>
                                    <div className="doc_name">
                                        <h style={{lineHeight: "120%", fontSize: "15px", fontWeight: "400"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                                        <h style={{color: "#8D8D8D"}}>150мб, 02.02.2022, 17:45</h>
                                    </div>
                                    <a className="del_btn" href="https://yandex.ru" style={{marginLeft: "3%", height: "50%"}}><img src={close} alt="close" width="170%"></img></a>
                                </div>
                                <div className="dates_docs_list">
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Дата документа</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>23.03.2019</h>
                                        </div>
                                    </div>
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Контрольная дата</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>27.07.2022</h>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <li className="docs_list_element">
                            <div style={{display: "flex", flexDirection: "row", height: "100%"}}>
                                <div style={{display: "flex", flexDirection: "row"}}>
                                    <img src={doc} alt="doc" width="55px" height="50px"></img>
                                    <div className="doc_name">
                                        <h style={{lineHeight: "120%", fontSize: "15px", fontWeight: "400"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                                        <h style={{color: "#8D8D8D"}}>150мб, 02.02.2022, 17:45</h>
                                    </div>
                                    <a className="del_btn" href="https://yandex.ru" style={{marginLeft: "3%", height: "50%"}}><img src={close} alt="close" width="170%"></img></a>
                                </div>
                                <div className="dates_docs_list">
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Дата документа</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>23.03.2019</h>
                                        </div>
                                    </div>
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Контрольная дата</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>27.07.2022</h>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <li className="docs_list_element">
                            <div style={{display: "flex", flexDirection: "row", height: "100%"}}>
                                <div style={{display: "flex", flexDirection: "row"}}>
                                    <img src={doc} alt="doc" width="55px" height="50px"></img>
                                    <div className="doc_name">
                                        <h style={{lineHeight: "120%", fontSize: "15px", fontWeight: "400"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                                        <h style={{color: "#8D8D8D"}}>150мб, 02.02.2022, 17:45</h>
                                    </div>
                                    <a className="del_btn" href="https://yandex.ru" style={{marginLeft: "3%", height: "50%"}}><img src={close} alt="close" width="170%"></img></a>
                                </div>
                                <div className="dates_docs_list">
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Дата документа</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>23.03.2019</h>
                                        </div>
                                    </div>
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Контрольная дата</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>27.07.2022</h>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <li className="docs_list_element">
                            <div style={{display: "flex", flexDirection: "row", height: "100%"}}>
                                <div style={{display: "flex", flexDirection: "row"}}>
                                    <img src={doc} alt="doc" width="55px" height="50px"></img>
                                    <div className="doc_name">
                                        <h style={{lineHeight: "120%", fontSize: "15px", fontWeight: "400"}}>Мы надеемся, что название файла может быть немного короче, а не вот эти три строчки</h>
                                        <h style={{color: "#8D8D8D"}}>150мб, 02.02.2022, 17:45</h>
                                    </div>
                                    <a className="del_btn" href="https://yandex.ru" style={{marginLeft: "3%", height: "50%"}}><img src={close} alt="close" width="170%"></img></a>
                                </div>
                                <div className="dates_docs_list">
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Дата документа</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>23.03.2019</h>
                                        </div>
                                    </div>
                                    <div className="date_choose">
                                        <img src={calendar} alt="calendar"></img>
                                        <div style={{display: "flex", flexDirection: "column"}}>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Контрольная дата</h>
                                            <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>27.07.2022</h>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
                <div className="date_all">
                    <div className="dates_docs_list_all">
                        <div className="date_choose">
                            <img src={calendar} alt="calendar"></img>
                            <div style={{display: "flex", flexDirection: "column"}}>
                                <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Дата документа</h>
                                <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>23.03.2019</h>
                            </div>
                        </div>
                        <div className="date_choose">
                            <img src={calendar} alt="calendar"></img>
                            <div style={{display: "flex", flexDirection: "column"}}>
                                <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "12px", lineHeight: "120%", color: "#031528"}}>Контрольная дата</h>
                                <h style={{fontStyle: "normal", fontWeight: "400", fontSize: "16px", lineHeight: "150%", color: "#B1B9C3", flex: "none", flexGrow: "0"}}>27.07.2022</h>
                            </div>
                        </div>
                    </div>
                    <button id="submit_date_all">
                        <h style={{color: "#3272C0", fontSize: "16px", fontWeight: "400"}}>Применить для всех</h>
                    </button>
                </div>
            </div>
            <img src={c51} alt="img" style={{marginLeft: "250px", marginTop: "470px"}}></img>
            <img src={c53} alt="img" style={{marginLeft: "450px", marginTop: "520px"}}></img>
            <img src={c52} alt="img" style={{marginLeft: "550px", marginTop: "320px"}}></img>
        </main>
      </body>
      );
  }

export default Dates;
