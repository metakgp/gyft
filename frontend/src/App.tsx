import React, { useState } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import MultiForm from "./components/MultiForm";
import { Toaster } from "react-hot-toast";
import Circles from "./components/Circles";
import hero from "./assets/hero-img.png";
import Modal from "./components/Modal";

const App: React.FC = () => {
    const [openModal, setOpenModal] = useState(false);
    return (
        <>
            <main>
                <Toaster position="bottom-center" />
                <Circles />
                <div id="wrapper">
                    <div className="wrapper-item">
                        <div id="wrapped">
                            <Header />
                            <MultiForm />
                        </div>
                        <Footer openModal={setOpenModal} />
                    </div>
                    <aside>
                        <img src={hero} alt="." />
                    </aside>
                </div>
            </main>
            {openModal && <Modal closeModal={setOpenModal} />}
        </>
    );
};

export default App;
