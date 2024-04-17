import axios from "axios";

type AnyError = unknown

function extractErrorMessage(error: AnyError): string {
    if (axios.isAxiosError(error)) {
        return error.response?.data?.message || error.message || 'An error occurred while fetching data'
    }
    else if (error instanceof Error) {
        return error.message
    }

    return 'An unknown error occurred'
}

export default extractErrorMessage