import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
import Modal from "./Modal";
import { useAppContext } from "../AppContext/AppContext";

const About: React.FC = () => {
    // const navigate = useNavigate();
    const [openModal, setOpenModal] = useState(false);
    const { logout, user } = useAppContext();

    return (
        <>
            <div className="help">
                <button
                    className="help-button"
                    onClick={() => setOpenModal(true)}
                >
                    Help
                </button>
                {user.ssoToken && (
                    <button onClick={logout} className="logout-button">
                        Logout
                    </button>
                )}
            </div>
            {openModal && <Modal closeModal={setOpenModal} />}
        </>
    );
};

export default About;
