import os
import shutil

def _find_chrome(user_given_path=None):
    """
    Checks the validity of a given path.
    If no path fiven, try to find a valid path.
    """

    if user_given_path is not None:
        if os.path.isfile(user_given_path):
            return user_given_path
        else:
            print('Could not find chrome in the given path.')
            exit(1)

    if os.name == 'nt':
        # Winwows system
        prefixes = [
            os.getenv('PROGRAMFILES(X86)'),
            os.getenv('PROGRAMFILES'),
            os.getenv('LOCALAPPDATA'),
        ]

        suffix = "Google\\Chrome\\Application\\chrome.exe"

        for prefix in prefixes:
            path_candidate = os.path.join(prefix, suffix)
            if os.path.isfile(path_candidate):
                return path_candidate

    else:
        # Other systems (not Windows)

        # test for the most common directory first
        if os.path.isfile("/usr/bin/chromium-browser"):
            return "/usr/bin/chromium-browser"

        # search for chromium-browser with a python equivalent of the `which` command
        which_result = shutil.which('chromium-browser')
        if os.path.isfile(which_result):
            return which_result

    print('Could not find a Chrome executable on this machine, please specify it yourself.')
    exit(1)

class HtmlToImage():

    # todo : check if output path exists on init or on attribute change

    def __init__(
        self,
        browser='chrome',
        chrome_path=None,
        firefox_path=None,
        output_path=os.getcwd(),
        size=(1920, 1080),
        temp_path=None,
    ):
        """
        """
        self.browser = browser
        self.chrome_path = chrome_path
        self.firefox_path = firefox_path
        self.output_path = output_path
        self.size = size
        self.temp_path = temp_path # calls the setter

        if self.browser == "chrome":
            self._render = self._chrome_render
            self.chrome_path = chrome_path # calls the setter

        elif self.browser == "firefox":
            raise NotImplementedError
        else:
            raise NotImplementedError
    
    @property
    def chrome_path(self):
        return self._chrome_path

    @chrome_path.setter
    def chrome_path(self, value):
        self._chrome_path = _find_chrome(value)

    @property
    def temp_path(self):
        return self._temp_path

    @temp_path.setter
    def temp_path(self, value):
        if value is None:
            temp_dir = os.environ['TMP'] if os.name == 'nt' else '/tmp'
            temp_dir = os.path.join(temp_dir, 'html2image')
        else:
            temp_dir = value
        
        # create the directory if it does not exist
        os.makedirs(temp_dir, exist_ok=True)

        self._temp_path = temp_dir
    
    @property
    def size(self):
        return tuple(int(i) for i in self._size.split(','))
    
    @size.setter
    def size(self, value):
        self._size = f'{value[0]},{value[1]}'

    def render(self, html_file, image_name):
        """

        """
        html_file = os.path.join(self.temp_path, html_file)
        self._render(output_file=image_name, input=html_file)

    def _chrome_render(self, output_file='render.png', input=''):
        """

        """

        # multiline str representing the command used to launch chrome in
        # headless mode and take a screenshot
        command = (
            f'"{self.chrome_path}" '
            f'--headless '
            f'--screenshot={os.path.join(self.output_path, output_file)} '
            f'--window-size={self._size} '
            f'--default-background-color=0 '
            f'{input}'
        )
        # print(command)
        os.system(command)

    def _firefox_render(self, output_file='render.png', input=''):
        """
        
        """
        raise NotImplementedError

    def url_to_img(self, url, output_file='render.png'):
        self._render(input=url, output_file=output_file)

    def load_str(self, css_content, as_filename):
        with open(os.path.join(self.temp_path, as_filename), 'w') as f:
            f.writelines(css_content)

    def load_file(self, src, as_filename=None):
        if as_filename is None:
            as_filename = os.path.basename(src)

        dest = os.path.join(self.temp_path, as_filename)
        shutil.copyfile(src, dest)


if __name__ == '__main__':
    pass
