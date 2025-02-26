import { useState } from "react";

export const useGeolocation = () => {
    const [locationInfo, setLocationInfo] = useState(null);
    const [locationError, setLocationError] = useState(null);

const {geolocation} = navigator;

const successFunc = (res) => {
    console.log (res);
    setLocationInfo (res.coords);
}

const errorFunc = (res) => {
    console.log(res);
    setLocationError(res.message);
}

if (!locationError && !locationInfo) {
    geolocation.getCurrentPosition(successFunc, errorFunc);
}

return {locationError, locationInfo}; 

}