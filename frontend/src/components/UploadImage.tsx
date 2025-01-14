import React, {useCallback} from 'react';
import { useDropzone } from 'react-dropzone';
import { BACKEND_URL } from './url';
import { toast } from 'react-hot-toast';
import { IAuth } from '../AppContext/AppContext';

type props = {
    setTimeTableFile: React.Dispatch<React.SetStateAction<Blob | undefined>>;
    setAuth: React.Dispatch<React.SetStateAction<IAuth>>;
    openModal: React.Dispatch<React.SetStateAction<boolean>>;
}

const UploadImage: React.FC<props> = ({ setTimeTableFile, setAuth, openModal }) => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = async () => {
                const base64String = reader.result as string;
                const formData = new URLSearchParams();
                formData.append('image', base64String);
                const res = await fetch(`${BACKEND_URL}/parse_image`, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: formData
                });

                if(!res.ok) {
                    toast.error("Unable to extract the timetable off the image. Please login to get your timetable");
                    return;
                }

                const blob = await res.blob();
                setTimeTableFile(blob);
                setAuth((prev) => ({
                    user: prev.user,
                    currentStep: 3
                }))
                openModal(false);

            };
            reader.readAsDataURL(file);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: {
        "image/*": ['.jpeg', '.jpg', '.png']
    }});


   return (
    <>
        <h2>Upload Image</h2>
        <p>
            Upload a screenshot of your timetable from ERP and we'll
            extract the timetable for you!
        </p>
        <h4>How to get your timetable?</h4>
        <ol>
            <li>Open the timetable page on ERP.</li>
            <li>Take a screenshot of the timetable.</li>
            <li>Upload the screenshot here.</li>
        </ol>
        <div {...getRootProps()} className="dropzone">
            <input {...getInputProps()} />
            {isDragActive ? (
                <div className='drop-image'>
                    Drop the image here ...
                </div>
            ) : (
                <div className='drop-image'>
                    Drag 'n' drop an image here, or click to select one
                </div>
            )}
        </div>
    </>
   ) 
}

export default UploadImage;