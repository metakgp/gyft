import React, { useState } from "react";
import { useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";

import { BACKEND_URL } from "./url";
import { toast } from "react-hot-toast";
import { useAppContext } from "../AppContext/AppContext";
import Spinner from "./Spinner";

const schema = yup.object().shape({
    securityAnswer: yup.string().required("Security answer is required!"),
    otp: yup.string().optional(),
});

interface IFormInput {
    securityAnswer: string;
    otp?: string;
}

const SecurityQueForm: React.FC = () => {
    const {
        register,
        handleSubmit,
        getValues,
        trigger,
        formState: { errors },
    } = useForm<IFormInput>({ resolver: yupResolver(schema) });
    const { user, setAuth } = useAppContext();

    const [otpRequested, setOtpRequested] = useState(false);
    const [loadingOTP, setLoadingOTP] = useState(false); 
    const [loadingLogin, setLoadingLogin] = useState(false); 

    const getOTP = async () => {
        const isValid = await trigger("securityAnswer");
        if (!isValid) return;
        const securityAns = getValues("securityAnswer");

        const formData = new URLSearchParams();
        formData.append("roll_number", user.rollNo);
        formData.append("password", user.password);
        formData.append("secret_answer", securityAns);

        try {
            setLoadingOTP(true);
            const res = await fetch(`${BACKEND_URL}/request-otp`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Session-Token": user.sessionToken!,
                },
                body: formData.toString(),
            });

            const resData = await res.json();

            if (!res.ok) {
                toast.error(resData.message);
                if (res.status == 400) {
                    return;
                }
                if (res.status == 401)
                    if (resData.message == "Invalid Password")
                        return setAuth((prev) => ({ ...prev, currentStep: 0 }));
                    else if(resData.message == "Invalid Security Question Answer")
                        return

                if (res.status == 500) throw new Error(resData.message);

                return;
            }

            setAuth((prev) => ({
                ...prev,
                user: { ...prev.user, securityAnswer: securityAns },
            }));
            setOtpRequested(true);
            toast.success(resData.message);
        } catch (error) {
            console.log(error);
            setOtpRequested(false);
        } finally {
            setLoadingOTP(false); 
        }
    };

    const login = async () => {
        const otp = getValues("otp");
        if (!otp || otp.length != 6) return toast.error("Invalid OTP Length");

        const login_data = new URLSearchParams();
        login_data.append("roll_number", user.rollNo!);
        login_data.append("password", user.password!);
        login_data.append("secret_answer", user.securityAnswer!);
        login_data.append("otp", otp);

        try {
            setLoadingLogin(true);
            const res = await fetch(`${BACKEND_URL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Session-Token": user.sessionToken!,
                },
                body: login_data.toString(),
            });

            const resData = await res.json();

            if (!res.ok) {
                toast.error(resData.message);
                if (res.status == 400) {
                    return;
                }
                if (res.status == 401)
                    if (resData.message == "Invalid Password" || resData.message == "Session isn't alive. PLease login again.")
                        return setAuth((prev) => ({ ...prev, currentStep: 0 }));
                if (resData.message == "Invalid OTP")
                    return setAuth((prev) => ({ ...prev, currentStep: 1 }));
                if (res.status == 500) throw new Error(resData.message);
            }

            sessionStorage.setItem("ssoToken", resData.ssoToken);
            setAuth((prev) => ({
                ...prev,
                currentStep: 2,
                user: { ...prev.user, ssoToken: resData.ssoToken },
            }));
            toast.success("Successfully logged in to ERP!");
        } catch (error) {
            console.error(error);
        } finally {
            setLoadingLogin(false); 
        }
    };

    const onSubmit = async () => {
        if (otpRequested) login();
        else getOTP();
    };

    return (
        <form className="login-form" onSubmit={handleSubmit(onSubmit)}>
            <div className="input-item">
                <label>{user.securityQuestion || "\u00A0"} :</label>
                <input
                    type="password"
                    placeholder="Enter your answer"
                    className={
                        errors.securityAnswer
                            ? "input-box input-error"
                            : "input-box"
                    }
                    {...register("securityAnswer")}
                ></input>
                <span className="input-error-msg">
                    {errors.securityAnswer?.message || "\u00A0"}
                </span>
            </div>
            <div className="input-item">
                <label>Enter OTP :</label>
                <input
                    type="text"
                    placeholder="Enter OTP sent to email"
                    className={
                        errors.otp ? "input-box input-error" : "input-box"
                    }
                    {...register("otp", {
                        required: otpRequested,
                        disabled: !otpRequested,
                    })}
                    style={
                        otpRequested
                            ? { cursor: "text" }
                            : { cursor: "not-allowed" }
                    }
                ></input>
                <span className="input-error-msg">
                    {errors.otp?.message || "\u00A0"}
                </span>
            </div>
            <div>
                <button className="submit-button" type="submit" disabled={loadingOTP || loadingLogin}>
                {loadingOTP || loadingLogin ? (
                        <Spinner />
                    ) : (
                        otpRequested ? "Login" : "Send OTP"
                    )}
                </button>
            </div>
        </form>
    );
};

export default SecurityQueForm;
