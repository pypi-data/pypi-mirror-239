import { LabIcon } from '@jupyterlab/ui-components';

import connectedSvgstr from '../static/icons/connected.svg';
import einblickSvgstr from '../static/icons/einblick.svg';
import notConnectedSvgstr from '../static/icons/notConnected.svg';

export const connectedIcon = new LabIcon({
  name: 'ai-einblick-prompt:connected',
  svgstr: connectedSvgstr
});

export const einblickIcon = new LabIcon({
  name: 'ai-einblick-prompt:einblick',
  svgstr: einblickSvgstr
});

export const notConnectedIcon = new LabIcon({
  name: 'ai-einblick-prompt:not-connected',
  svgstr: notConnectedSvgstr
});
