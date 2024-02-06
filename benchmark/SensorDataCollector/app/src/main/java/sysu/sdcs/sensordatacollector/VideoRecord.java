package sysu.sdcs.sensordatacollector;
import android.hardware.Camera;
import android.media.MediaRecorder;
import java.io.IOException;
public class VideoRecord {
    private MediaRecorder mediaRecorder;
    private Camera camera;
    public void startRecording(String outputFile) {;
        camera = Camera.open();
        camera.unlock();
        mediaRecorder = new MediaRecorder();

        mediaRecorder.setVideoSource(MediaRecorder.VideoSource.DEFAULT);
        mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.DEFAULT);
        mediaRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.DEFAULT);
        mediaRecorder.setVideoSize(320, 240);

        mediaRecorder.setOutputFile(outputFile + ".3gp");

        try {
            mediaRecorder.prepare();
            mediaRecorder.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void stopRecording() {
        if (mediaRecorder != null) {
            mediaRecorder.stop();
            mediaRecorder.reset();
            mediaRecorder.release();
            mediaRecorder = null;
        }
    }
}