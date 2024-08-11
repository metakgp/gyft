import React from "react";

let circles_list = [
    {
        position: [10, 15],
        color: "0 0 400px 140px rgba(0, 133, 255, 1)",
    },
    {
        position: [10, 90],
        color: "0 0 100px 100px rgba(0, 255, 102, 0.72)",
    },
    { position: [40, 40], color: "0 0 150px 100px #FFD447" },
    {
        position: [100, 10],
        color: "0 0 250px 150px rgba(204, 0, 255, 0.75)",
    },
    {
        position: [80, 90],
        color: "0 0 200px 80px rgba(204, 0, 255, 1)",
    },
];

const Circles: React.FC = () => {
    return (
        <div className="circle-container">
            {circles_list.map((x, i) => (
                <div
                    key={i}
                    className="circle"
                    style={{
                        top: `${x.position[0]}%`,
                        left: `${x.position[1]}%`,
                        boxShadow: x.color,
                    }}
                />
            ))}
        </div>
    );
};
export default Circles;
