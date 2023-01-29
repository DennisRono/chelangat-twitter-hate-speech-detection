import axios from "axios"

let baseURL = 'http://localhost:5000/'

export const api = async (method = 'GET', slug = '', data = {}) => {
    let config = {
        method: method,
        url: baseURL+slug,
        headers: { 
            'Content-Type': 'application/json'
        },
        data : JSON.stringify(data)
    };
    const response = await axios(config)
    return response.data
}