package com.wh.andy.medicaltreatment.robot;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import com.wh.andy.medicaltreatment.robot.R;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.OnClick;

public class MainActivity extends AppCompatActivity {
    @BindView(R.id.tv_check)
    TextView tv_check;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);
        initView();
    }

    private void initView() {

    }

    @OnClick(R.id.tv_check)
    public  void onClick(View view){
        Intent intent=new Intent(this, CheckTypeBloodPortraitActivity.class);
        startActivity(intent);
    }
}