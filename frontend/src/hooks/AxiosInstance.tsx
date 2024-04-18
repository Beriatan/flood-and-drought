import axios from "axios";


const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || 'http://flought-fyp.eu-west-1.elasticbeanstalk.com',
})

export default axiosInstance