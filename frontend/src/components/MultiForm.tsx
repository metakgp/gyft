import React from "react";
import RollForm from "./RollForm";
import SecurityQueForm from "./SecurityQueForm";
import { useAppContext } from "../AppContext/AppContext";
import Timetable from "./Timetable";
import ErrorPage from "./ErrorPage";

const MultiForm: React.FC = () => {
    const { currentStep, user } = useAppContext();
    if (currentStep == 2 && user.sessionToken && user.ssoToken)
        return <Timetable />;
    if (currentStep == 1 && user.sessionToken && user.securityQuestion)
        return <SecurityQueForm />;
    if (currentStep == 0) return <RollForm />;
    return <ErrorPage />;
};

export default MultiForm;
