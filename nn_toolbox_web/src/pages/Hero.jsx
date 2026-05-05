import Lottie from "lottie-react";
import animationData from "../assets/neuron.json";

export default function Hero() {
  return (
    <div className="w-full h-screen flex items-center justify-center bg-black">
      <div className="w-full h-full flex items-center justify-center">
        <Lottie 
          animationData={animationData} 
          loop={true}
          style={{
            width: "100%",
            height: "100%",
            maxWidth: "800px"
          }}
        />
      </div>
    </div>
  );
}
