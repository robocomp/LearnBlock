package robopad;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.SubMenu;
import android.view.View;
import android.view.View.OnTouchListener;
import android.widget.ActionMenuView;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.TextView;

import ricardo.joystick.robopad.R;

public class Main extends Activity {
    RelativeLayout mLayoutJoystick;
    TextView mTextViewDirection;
    JoyStickClass joystick;
    ProgressBar mProgressBar1;
    ProgressBar mProgressBar2;
    ProgressBar mProgressBar3;
    ProgressBar mProgressBar4;


    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        mTextViewDirection = (TextView) findViewById(R.id.textView5);

        mProgressBar1 = (ProgressBar) findViewById(R.id.progressBar1);
        mProgressBar2 = (ProgressBar) findViewById(R.id.progressBar2);
        mProgressBar3 = (ProgressBar) findViewById(R.id.progressBar3);
        mProgressBar4 = (ProgressBar) findViewById(R.id.progressBar4);




        mLayoutJoystick = (RelativeLayout) findViewById(R.id.layout_joystick);

        joystick = new JoyStickClass(getApplicationContext(), mLayoutJoystick, R.drawable.image_button);
        joystick.setStickSize(100, 100);
        joystick.setLayoutSize(300, 300);
        joystick.setLayoutAlpha(250);
        joystick.setStickAlpha(250);
        joystick.setOffset(50);
        joystick.setMinimumDistance(100);

        setStateBar();

        mLayoutJoystick.setOnTouchListener(new OnTouchListener() {
            public boolean onTouch(View arg0, MotionEvent arg1) {
                joystick.drawStick(arg1);
                if (arg1.getAction() == MotionEvent.ACTION_DOWN || arg1.getAction() == MotionEvent.ACTION_MOVE) {

                    switch (joystick.get8Direction()) {

                        case JoyStickClass.STICK_UP:
                            mTextViewDirection.setText("Up");
                            break;
                        case JoyStickClass.STICK_UPRIGHT:
                            mTextViewDirection.setText("Up Right");
                            break;
                        case JoyStickClass.STICK_RIGHT:
                            mTextViewDirection.setText("Right");
                            break;
                        case JoyStickClass.STICK_DOWNRIGHT:
                            mTextViewDirection.setText("Down Right");
                            break;
                        case JoyStickClass.STICK_DOWN:
                            mTextViewDirection.setText("Down");
                            break;
                        case JoyStickClass.STICK_DOWNLEFT:
                            mTextViewDirection.setText("Down Left");
                            break;
                        case JoyStickClass.STICK_LEFT:
                            mTextViewDirection.setText("Left");
                            break;
                        case JoyStickClass.STICK_UPLEFT:
                            mTextViewDirection.setText("Up Left");
                            break;
                        case JoyStickClass.STICK_NONE:
                            mTextViewDirection.setText("Center");
                            break;
                        default:
                            mTextViewDirection.setText("");
                            break;
                    }
                }
                return true;
            }

        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.menu_settings:

            default:
                return super.onOptionsItemSelected(item);
        }
    }


    public void setStateBar() {
        mProgressBar1.setProgress(90);
        mProgressBar2.setProgress(10);
        mProgressBar3.setProgress(30);
        mProgressBar4.setProgress(60);

    }

    private robopad.HelloPrx createProxy()
    {
        String host = _hostname.getText().toString().trim();
        assert (host.length() > 0);
        // Change the preferences if necessary.
        if(!_prefs.getString(HOSTNAME_KEY, DEFAULT_HOST).equals(host))
        {
            SharedPreferences.Editor edit = _prefs.edit();
            edit.putString(HOSTNAME_KEY, host);
            edit.commit();
        }

        String s = "hello:tcp -h " + host + " -p 10000:ssl -h " + host + " -p 10001:udp -h " + host + " -p 10000";
        Ice.ObjectPrx prx = _communicator.stringToProxy(s);
        prx = _deliveryMode.apply(prx);
        int timeout = _timeout.getProgress();
        if(timeout != 0)
        {
            prx = prx.ice_timeout(timeout);
        }
        return Demo.HelloPrxHelper.uncheckedCast(prx);
    }

}
