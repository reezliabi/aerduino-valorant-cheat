#include <hidboot.h>
#include "ImprovedMouse.h"

struct CUSTOMMOUSEINFO
{
  uint8_t buttons;
  int8_t dX;
  int8_t dY;
  int8_t wheel;
};

class MouseRptParser : public MouseReportParser
{
  union
  {
    CUSTOMMOUSEINFO mouseInfo;
    uint8_t bInfo[sizeof(CUSTOMMOUSEINFO)];
  } prevState;

protected:
  void Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf);

  void OnMouseMove(CUSTOMMOUSEINFO *mi);
  void OnWheelMove(CUSTOMMOUSEINFO *mi);

  void OnLeftButtonUp(CUSTOMMOUSEINFO *mi);
  void OnLeftButtonDown(CUSTOMMOUSEINFO *mi);

  void OnRightButtonUp(CUSTOMMOUSEINFO *mi);
  void OnRightButtonDown(CUSTOMMOUSEINFO *mi);

  void OnMiddleButtonUp(CUSTOMMOUSEINFO *mi);
  void OnMiddleButtonDown(CUSTOMMOUSEINFO *mi);

  void OnPrevButtonUp(CUSTOMMOUSEINFO *mi);
  void OnPrevButtonDown(CUSTOMMOUSEINFO *mi);

  void OnNextButtonUp(CUSTOMMOUSEINFO *mi);
  void OnNextButtonDown(CUSTOMMOUSEINFO *mi);
};