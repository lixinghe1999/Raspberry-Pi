package sysu.sdcs.sensordatacollector;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.otaliastudios.cameraview.CameraListener;
import com.otaliastudios.cameraview.CameraView;
import com.otaliastudios.cameraview.PictureResult;
import com.otaliastudios.cameraview.VideoResult;
import com.otaliastudios.cameraview.controls.Facing;
import com.otaliastudios.cameraview.controls.Flash;
import com.otaliastudios.cameraview.controls.Mode;

import java.io.File;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {

    private static final int REQ_CODE_PERMISSION_EXTERNAL_STORAGE = 0x1111;
    private static final int REQ_CODE_PERMISSION_SENSOR = 0x2222;

    private SensorManager sensorManager;
    private SensorListener sensorListener;
    private Sensor accelerometerSensor;
    private Sensor gyroscopeSensor;

    private Button btn_imu, btn_back, btn_mic, btn_front;
    private EditText edt_path;
    private TextView tv_state;
    private TextView tv_record;

    private ScheduledFuture future;
    private String file_name = "";
    private String cap_records = "";
    private PlayRecord playrecorder;
    public static String file_path = Environment.getExternalStorageDirectory().getAbsolutePath()
            + "/SensorData/";
    private CameraView camera;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        init();
        btn_imu.setOnClickListener(imu_listener);
        btn_back.setOnClickListener(back_listener);
        btn_mic.setOnClickListener(mic_listener);
        btn_front.setOnClickListener(front_listener);

        camera = findViewById(R.id.camera);
        camera.setLifecycleOwner(this);
        camera.addCameraListener(new CameraListener() {
            @Override
            public void onPictureTaken(PictureResult result) {
                // A Picture was taken!
            }

            @Override
            public void onVideoTaken(VideoResult result) {
                // A Video was taken!
            }

            // And much more
        });
    }

    public void init(){
        btn_imu = findViewById(R.id.btn_imu);
        edt_path = findViewById(R.id.edt_pathID);
        tv_state = findViewById(R.id.state);
        tv_record = findViewById(R.id.record);

        sensorListener = new SensorListener();
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accelerometerSensor = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        gyroscopeSensor = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);

        btn_back = findViewById(R.id.btn_back);
        btn_mic = findViewById(R.id.btn_mic);
        btn_front = findViewById(R.id.btn_front);
        permissionCheck();
    }

    public void permissionCheck(){
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                != PackageManager.PERMISSION_GRANTED){
            //申请WRITE_EXTERNAL_STORAGE权限
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                    REQ_CODE_PERMISSION_EXTERNAL_STORAGE);
        }
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.BODY_SENSORS)
                != PackageManager.PERMISSION_GRANTED){
            //申请BODY_SENSOR权限
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.BODY_SENSORS},
                    REQ_CODE_PERMISSION_SENSOR);
        }
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED){
            //申请CAMERA权限
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA},
                    REQ_CODE_PERMISSION_SENSOR);
        }
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED){
            //申请CAMERA权限
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO},
                    REQ_CODE_PERMISSION_SENSOR);
        }
    }
    private View.OnClickListener mic_listener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(edt_path.getText().toString().equals("") ||
                    edt_path.getText().toString() == null) {
                Toast.makeText(MainActivity.this, "path ID 不能为空", Toast.LENGTH_SHORT).show();
            }
            else if(btn_mic.getText().toString().equals("Microphone")){
                camera.close();
                playrecorder = new PlayRecord();
                file_name = file_path + "/" + edt_path.getText().toString() + "-" + "mic-" +
                        (UUIDUtil.generateRandomString(4));
                playrecorder.startRecordingWhilePlayingMusic(file_name);
                tv_state.setText("传感器数据正在采集中\n" + "当前采集路径为: " + edt_path.getText().toString());
                btn_mic.setText("stop");
            }
            else{
                playrecorder.stopRecordingWhilePlayingMusic(file_name);
                cap_records = file_name;
                tv_record.setText(cap_records);
                Toast.makeText(MainActivity.this, "传感器数据保存成功", Toast.LENGTH_SHORT).show();
                btn_mic.setText("Microphone");
                tv_state.setText("点击按钮开始采集\n");
            }

        }
    };

    private View.OnClickListener back_listener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(edt_path.getText().toString().equals("") ||
                    edt_path.getText().toString() == null) {
                Toast.makeText(MainActivity.this, "path ID 不能为空", Toast.LENGTH_SHORT).show();
            }
            else if(btn_back.getText().toString().equals("Back camera")){
                camera.open();
                camera.setFacing(Facing.BACK);

                file_name = file_path + "/" + edt_path.getText().toString() + "-" + "back-" +
                        (UUIDUtil.generateRandomString(4)) + ".mp4";
                camera.setMode(Mode.VIDEO);
                camera.takeVideo(new File(file_name));
                camera.setFlash(Flash.TORCH);
                tv_state.setText("传感器数据正在采集中\n" + "当前采集路径: " + edt_path.getText().toString());
                btn_back.setText("stop");
            }
            else{
                camera.stopVideo();
                camera.close();
                camera.setFlash(Flash.OFF);
                cap_records = file_name;
                tv_record.setText(cap_records);
                Toast.makeText(MainActivity.this, "传感器数据保存成功", Toast.LENGTH_SHORT).show();
                btn_back.setText("Back camera");
                tv_state.setText("点击按钮开始采集\n");
            }

        }
    };
    private View.OnClickListener front_listener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(edt_path.getText().toString().equals("") ||
                    edt_path.getText().toString() == null) {
                Toast.makeText(MainActivity.this, "path ID 不能为空", Toast.LENGTH_SHORT).show();
            }
            else if(btn_front.getText().toString().equals("Front camera")){
                camera.open();
                camera.setFacing(Facing.FRONT);

                file_name = file_path + "/" + edt_path.getText().toString() + "-" + "front-" +
                        (UUIDUtil.generateRandomString(4)) + ".mp4";
                camera.setMode(Mode.VIDEO);
                camera.takeVideo(new File(file_name));
                tv_state.setText("传感器数据正在采集中\n" + "当前采集路径为: " + edt_path.getText().toString());
                btn_front.setText("stop");
            }
            else{
                camera.stopVideo();
                camera.close();
                cap_records = file_name;
                tv_record.setText(cap_records);
                Toast.makeText(MainActivity.this, "传感器数据保存成功", Toast.LENGTH_SHORT).show();
                btn_front.setText("Front camera");
                tv_state.setText("点击按钮开始采集\n");
            }

        }
    };
    private View.OnClickListener imu_listener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(edt_path.getText().toString().equals("") ||
                    edt_path.getText().toString() == null) {
                Toast.makeText(MainActivity.this, "path ID 不能为空", Toast.LENGTH_SHORT).show();
            }
            else if(btn_imu.getText().toString().equals("IMU")){
                camera.close();
                if(!sensorManager.registerListener(sensorListener, accelerometerSensor, SensorManager.SENSOR_DELAY_FASTEST ))
                    Toast.makeText(MainActivity.this, "加速度传感器不可用", Toast.LENGTH_SHORT).show();
                if(!sensorManager.registerListener(sensorListener, gyroscopeSensor, SensorManager.SENSOR_DELAY_FASTEST))
                    Toast.makeText(MainActivity.this, "陀螺仪不可用", Toast.LENGTH_SHORT).show();

                InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
                if (imm != null) {
                    imm.hideSoftInputFromWindow(getWindow().getDecorView().getWindowToken(), 0);
                }

                tv_state.setText("传感器数据正在采集中\n" + "当前采集路径为: " + edt_path.getText().toString());
                btn_imu.setText("stop");
                file_name = edt_path.getText().toString() + "-" + "imu-" +
                        (UUIDUtil.generateRandomString(4))+ ".csv";
                FileUtil.saveSensorData(file_name, SensorData.getFileHead());
                ScheduledExecutorService service = Executors.newScheduledThreadPool(5);
                future = service.scheduleAtFixedRate(new DataSaveTask(file_name), 5, 5, TimeUnit.SECONDS);
            }
            else{
                future.cancel(true);
                sensorManager.unregisterListener(sensorListener);
                if(FileUtil.saveSensorData(file_name, SensorData.getAccGyroDataStr())){
                    cap_records = file_name;
                    tv_record.setText(cap_records);
                    tv_state.setText("");
                    Toast.makeText(MainActivity.this, "传感器数据保存成功", Toast.LENGTH_SHORT).show();
                }
                else
                    Toast.makeText(MainActivity.this, "传感器数据保存失败", Toast.LENGTH_SHORT).show();
                SensorData.clear();
                btn_imu.setText("IMU");
                tv_state.setText("点击按钮开始采集\n");
            }

        }
    };

    //权限申请
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case REQ_CODE_PERMISSION_EXTERNAL_STORAGE: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // User agree the permission
                } else {
                    // User disagree the permission
                    Toast.makeText(MainActivity.this, "请打开存储权限", Toast.LENGTH_LONG).show();
                }
            }
            case REQ_CODE_PERMISSION_SENSOR: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    // User agree the permission
                }
                else {
                    // User disagree the permission
                    Toast.makeText(this, "请打开传感器权限", Toast.LENGTH_LONG).show();
                }
            }
            break;
        }
    }

}