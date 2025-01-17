import React, { useState } from "react";
import { BACKEND_URL } from "./url";
import { toast } from "react-hot-toast";
import { useAppContext } from "../AppContext/AppContext";
import Spinner from "./Spinner";

type props = {
    file?: Blob;
};

const Timetable: React.FC<props> = ({ file }) => {
    const { user, logout } = useAppContext();
    const [isLoading, setLoading] = useState(false);

    const getTimetable = async (
        e: React.MouseEvent<HTMLButtonElement, MouseEvent>
    ) => {
        e.preventDefault();
        const formData = new URLSearchParams();
        formData.append("roll_number", user.rollNo);

        try {
            let blob = new Blob();
            let filename = "";
            if(!file) {
                if (!user.ssoToken) return;

                const res = await fetch(`${BACKEND_URL}/timetable`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "SSO-Token": user.ssoToken,
                    },
                    body: formData.toString(),
                });

                if (!res.ok) {
                    const resData = await res.json();
                    toast.error(resData.message);
                    if (res.status == 401)
                        if (
                            resData.message ==
                            "Session isn't alive. PLease login again."
                        )
                            logout();
                    return;
                }

                filename = `${user.rollNo}_timetable.ics`;
                blob = await res.blob();
            } else {
                filename = "timetable.ics";
                blob = file;
            }

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (error) {
            toast.error(`Error fetching timetable!`);
            console.error("Error fetching timetable", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="timetable-container">
            <h2>{file ? "Time Table Extraction Successful!" : "Login Successful!"}</h2>
            <p>
                Download your timetable for current
                semester in .ics format which can be imported into other
                calendar applications like Google Calendar
            </p>
            <div className="timetable">
                <button
                    className="download-button"
                    onClick={(e) => getTimetable(e)}
                    disabled={isLoading}
                >
                    {isLoading ? <Spinner /> : "Download Timetable"}
                </button>
            </div>
        </div>
    );
};

export default Timetable;
