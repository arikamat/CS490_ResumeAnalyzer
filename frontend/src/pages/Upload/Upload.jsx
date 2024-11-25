import FileUpload from "./FileUpload";
import JobDescription from "./JobDescription";

import '../../assets/global.css';
// import useAuth from "../../hooks/useAuth";
function Upload() {
    // useAuth();
    return (
        <div className={'mainContainer'}>
            <FileUpload />
            <JobDescription />
        </div>


    );
}

export default Upload;