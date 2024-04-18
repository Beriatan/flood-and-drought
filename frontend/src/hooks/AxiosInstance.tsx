import axios from "axios";


const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || 'http://172.17.0.2:5000',
})

export default axiosInstance