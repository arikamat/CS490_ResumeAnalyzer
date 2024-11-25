import FileUpload from "./FileUpload";
import JobDescription from "./JobDescription";

import '../../assets/Global.css';
function Upload(){
    return (
        <div className={'mainContainer'}>
            <FileUpload/>
            <JobDescription/>
        </div>
            
        
    );
}

export default Upload;