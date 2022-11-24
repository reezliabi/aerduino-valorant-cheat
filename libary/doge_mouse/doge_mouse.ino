#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

#include "hidcustom.h"

#define CHECK_BIT(var, pos) ((var)&pos)

signed char leftMouseButton = 0;
signed char rightMouseButton = 0;
signed char middleMouseButton = 0;
signed char prevMouseButton = 0;
signed char nextMouseButton = 0;

signed char wheel = 0;
int dx = 0;
int dy = 0;

void MouseRptParser::Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf)
{
  CUSTOMMOUSEINFO *pmi = (CUSTOMMOUSEINFO *)buf;

  if (CHECK_BIT(prevState.mouseInfo.buttons, MOUSE_LEFT) != CHECK_BIT(pmi->buttons, MOUSE_LEFT))
  {
    if (CHECK_BIT(pmi->buttons, MOUSE_LEFT))
    {
      OnLeftButtonDown(pmi);
    }
    else
    {
      OnLeftButtonUp(pmi);
    }
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, MOUSE_RIGHT) != CHECK_BIT(pmi->buttons, MOUSE_RIGHT))
  {
    if (CHECK_BIT(pmi->buttons, MOUSE_RIGHT))
    {
      OnRightButtonDown(pmi);
    }
    else
    {
      OnRightButtonUp(pmi);
    }
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, MOUSE_MIDDLE) != CHECK_BIT(pmi->buttons, MOUSE_MIDDLE))
  {
    if (CHECK_BIT(pmi->buttons, MOUSE_MIDDLE))
    {
      OnMiddleButtonDown(pmi);
    }
    else
    {
      OnMiddleButtonUp(pmi);
    }
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, MOUSE_PREV) != CHECK_BIT(pmi->buttons, MOUSE_PREV))
  {
    if (CHECK_BIT(pmi->buttons, MOUSE_PREV))
    {
      OnPrevButtonDown(pmi);
    }
    else
    {
      OnPrevButtonUp(pmi);
    }
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, MOUSE_NEXT) != CHECK_BIT(pmi->buttons, MOUSE_NEXT))
  {
    if (CHECK_BIT(pmi->buttons, MOUSE_NEXT))
    {
      OnNextButtonDown(pmi);
    }
    else
    {
      OnNextButtonUp(pmi);
    }
  }

  if (pmi->dX || pmi->dY)
  {
    OnMouseMove(pmi);
  }

  if (len > 3)
  {
    OnWheelMove(pmi);
    prevState.bInfo[3] = buf[3];
  }

  prevState.bInfo[0] = buf[0];
}

void MouseRptParser::OnMouseMove(CUSTOMMOUSEINFO *mi)
{
  dx = mi->dX;
  dy = mi->dY;
}

void MouseRptParser::OnWheelMove(CUSTOMMOUSEINFO *mi)
{
  wheel = mi->wheel;
}

void MouseRptParser::OnLeftButtonDown(CUSTOMMOUSEINFO *mi)
{
  leftMouseButton = 1;
}

void MouseRptParser::OnLeftButtonUp(CUSTOMMOUSEINFO *mi)
{
  leftMouseButton = 0;
}

void MouseRptParser::OnRightButtonDown(CUSTOMMOUSEINFO *mi)
{
  rightMouseButton = 1;
}

void MouseRptParser::OnRightButtonUp(CUSTOMMOUSEINFO *mi)
{
  rightMouseButton = 0;
}

void MouseRptParser::OnMiddleButtonDown(CUSTOMMOUSEINFO *mi)
{
  middleMouseButton = 1;
}

void MouseRptParser::OnMiddleButtonUp(CUSTOMMOUSEINFO *mi)
{
  middleMouseButton = 0;
}

void MouseRptParser::OnPrevButtonDown(CUSTOMMOUSEINFO *mi)
{
  prevMouseButton = 1;
}

void MouseRptParser::OnPrevButtonUp(CUSTOMMOUSEINFO *mi)
{
  prevMouseButton = 0;
}

void MouseRptParser::OnNextButtonDown(CUSTOMMOUSEINFO *mi)
{
  nextMouseButton = 1;
}

void MouseRptParser::OnNextButtonUp(CUSTOMMOUSEINFO *mi)
{
  nextMouseButton = 0;
}

#include <usbhub.h>

USB Usb;
USBHub Hub(&Usb);
HIDBoot<USB_HID_PROTOCOL_MOUSE> HidMouse(&Usb);

MouseRptParser Prs;

byte inBytes[2];

int16_t coord[2];

int8_t i = 0;
int8_t j = 0;
int8_t e = 0;
int8_t temp = 0;
int8_t clipping[8];

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(1);

  uint8_t attempts = 30;
  while (!Serial && attempts--)
    delay(100);

  Usb.Init();
  HidMouse.SetReportParser(0, &Prs);
  Mouse.begin();
}

void loop()
{
  dx = 0;
  dy = 0;
  wheel = 0;

  Usb.Task();

  if (leftMouseButton == 0)
    Mouse.release(MOUSE_LEFT);
  else if (leftMouseButton == 1)
    Mouse.press(MOUSE_LEFT);

  if (rightMouseButton == 0)
    Mouse.release(MOUSE_RIGHT);
  else if (rightMouseButton == 1)
    Mouse.press(MOUSE_RIGHT);

  if (middleMouseButton == 0)
    Mouse.release(MOUSE_MIDDLE);
  else if (middleMouseButton == 1)
    Mouse.press(MOUSE_MIDDLE);

  if (prevMouseButton == 0)
    Mouse.release(MOUSE_PREV);
  else if (prevMouseButton == 1)
    Mouse.press(MOUSE_PREV);

  if (nextMouseButton == 0)
    Mouse.release(MOUSE_NEXT);
  else if (nextMouseButton == 1)
    Mouse.press(MOUSE_NEXT);

  memset(coord, 0, sizeof(coord));
  
  
      if (Serial.available() > 4) {
        byte bytes[4];
        for (byte i = 0; i < 4; i++) {
          bytes[i] = Serial.read();
        }
        if ( (bytes[0] == 0x7E) && (bytes[3] == 0x7E)) {
		  uint8_t data[2];
          data[0] = bytes[1];
          data[1] = bytes[2];
          Mouse.move(data[0], data[1], 0);
        }
		
		if ( (bytes[0] == 0x7B) && (bytes[3] == 0x7B)) {
		  uint8_t data[2];
          data[0] = bytes[1];
          data[1] = bytes[2];
          Mouse.move(-data[0], -data[1], 0);
        }

        if ( (bytes[0] == 0x5E) && (bytes[3] == 0x5E)) {
          Mouse.click(); 

        }
	  
    }	
	
	
  else
    Mouse.move(dx, dy, wheel);
}