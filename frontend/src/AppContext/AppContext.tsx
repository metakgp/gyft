import React, { useState, createContext, useContext } from "react";

interface IProps {
    children: React.ReactNode;
}
interface IUser {
    rollNo: string;
    password: string;
    securityQuestion: string;
    securityAnswer: string;
    ssoToken: string | null;
    sessionToken: string | null;
}

interface IAuth {
    user: IUser;
    currentStep: number;
}

interface IContext {
    authState: IAuth;
    setAuth: React.Dispatch<React.SetStateAction<IAuth>>;
    logout: () => void;
}

const DEFAULT_USER: IUser = {
    rollNo: sessionStorage.getItem("rollNo") || "",
    password: "",
    securityQuestion: "",
    securityAnswer: "",
    ssoToken: sessionStorage.getItem("ssoToken") || "",
    sessionToken: sessionStorage.getItem("sessionToken") || "",
};

export const AppContext = createContext<IContext | null>(null);

export const AppProvider: React.FC<IProps> = ({ children }) => {
    const [authState, setAuth] = useState<IAuth>({
        user: DEFAULT_USER,
        currentStep: DEFAULT_USER.ssoToken ? 2 : 0,
    });

    const logout = () => {
        sessionStorage.removeItem("ssoToken");
        sessionStorage.removeItem("sessionToken");
        setAuth({ user: DEFAULT_USER, currentStep: 0 });
    };

    return (
        <AppContext.Provider value={{ authState, setAuth, logout }}>
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error("useAppContext must be used within an AppProvider");
    }
    return {
        ...context.authState,
        setAuth: context.setAuth,
        logout: context.logout,
    };
};
