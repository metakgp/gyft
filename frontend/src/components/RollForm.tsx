import React from "react";
import { useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { BACKEND_URL } from "./url";
import { toast } from "react-hot-toast";
import Spinner from "./Spinner";
import { useAppContext } from "../AppContext/AppContext";

interface IFormInput {
    roll_number: string;
    password: string;
}

const schema = yup.object().shape({
    roll_number: yup
        .string()
        .required("Roll number is required!")
        .matches(/^\d{2}[A-Z]{2}[A-Z0-9]{5}$/, "Please enter valid roll number!"),
    password: yup.string().required("Password is required!"),
});

const RollForm: React.FC = () => {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<IFormInput>({ resolver: yupResolver(schema) });

    const { setAuth } = useAppContext();

    const getSecurityQuestion = async (data: IFormInput) => {
        try {
            const formData = new URLSearchParams();
            formData.append("roll_number", data.roll_number);
            formData.append("password", data.password);

            const res = await fetch(`${BACKEND_URL}/secret-question`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: formData,
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
                if (res.status == 500) throw new Error(resData.message);
            }

            sessionStorage.setItem("sessionToken", resData.SESSION_TOKEN);
            sessionStorage.setItem("rollNo", data.roll_number);

            toast.success("Fetched security question!");
            setAuth((prev) => ({
                user: {
                    ...prev.user,
                    password: data.password,
                    rollNo: data.roll_number,
                    securityQuestion: resData.SECRET_QUESTION,
                    sessionToken: resData.SESSION_TOKEN,
                },
                currentStep: 1,
            }));
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit(getSecurityQuestion)}>
                <div className="input-item">
                    <label>Roll number :</label>
                    <input
                        type="text"
                        placeholder="Roll number for ERP"
                        className={
                            errors.roll_number
                                ? "input-box input-error"
                                : "input-box"
                        }
                        {...register("roll_number")}
                    />

                    <span className="input-error-msg">
                        {errors.roll_number?.message || "\u00A0"}
                    </span>
                </div>
                <div className={`input-item`}>
                    <label>Password :</label>
                    <input
                        type="password"
                        placeholder="Password for ERP login"
                        className={
                            errors.password
                                ? "input-box input-error"
                                : "input-box"
                        }
                        {...register("password")}
                    />

                    <span className="input-error-msg">
                        {errors.password?.message || "\u00A0"}
                    </span>
                </div>
                <button type="submit" className="submit-button" disabled={isSubmitting}>
                    {isSubmitting ? <Spinner /> : "Get security question"}
                </button>
            </form>
        </>
    );
};

export default RollForm;
