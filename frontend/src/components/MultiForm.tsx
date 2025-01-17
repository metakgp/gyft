import React, { useState } from "react";
import RollForm from "./RollForm";
import SecurityQueForm from "./SecurityQueForm";
import { useAppContext } from "../AppContext/AppContext";
import Timetable from "./Timetable";
import ErrorPage from "./ErrorPage";

type props = {
    openModal: React.Dispatch<React.SetStateAction<boolean>>;
    setModalContent: React.Dispatch<React.SetStateAction<React.ReactNode | undefined>>;
};

const MultiForm: React.FC<props> = ({ openModal, setModalContent }) => {
    const { currentStep, user } = useAppContext();
    const [ timeTableFile, setTimeTableFile ] = useState(undefined as Blob | undefined);
    if(currentStep == 3 && timeTableFile) return <Timetable file={timeTableFile} />;
    if (currentStep == 2 && user.sessionToken && user.ssoToken)
        return <Timetable />;
    if (currentStep == 1 && user.sessionToken && user.securityQuestion)
        return <SecurityQueForm />;
    if (currentStep == 0) return <RollForm openModal={openModal} setModalContent={setModalContent} setTimeTableFile={setTimeTableFile} />;
    return <ErrorPage />;
};

export default MultiForm;
